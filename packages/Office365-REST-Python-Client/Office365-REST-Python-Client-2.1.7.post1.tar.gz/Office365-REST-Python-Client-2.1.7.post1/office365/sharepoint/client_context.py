from office365.runtime.client_query import DeleteEntityQuery, UpdateEntityQuery
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.context_web_information import ContextWebInformation
from office365.runtime.odata.json_light_format import JsonLightFormat
from office365.runtime.odata.odata_metadata_level import ODataMetadataLevel
from office365.runtime.utilities.http_method import HttpMethod
from office365.runtime.utilities.request_options import RequestOptions
from office365.sharepoint.site import Site
from office365.sharepoint.web import Web


class ClientContext(ClientRuntimeContext):
    """SharePoint client context"""

    def __init__(self, base_url, auth_context):
        if base_url.endswith("/"):
            base_url = base_url[:len(base_url) - 1]
        super(ClientContext, self).__init__(base_url + "/_api/", auth_context)
        self.__web = None
        self.__site = None
        self.contextWebInformation = None
        self.json_format = JsonLightFormat(ODataMetadataLevel.Verbose)

    def ensure_form_digest(self, request_options):
        if not self.contextWebInformation:
            self.request_form_digest()
        request_options.set_header('X-RequestDigest', self.contextWebInformation.formDigestValue)

    def request_form_digest(self):
        """Request Form Digest"""
        request = RequestOptions(self.serviceRootUrl + "contextinfo")
        request.method = HttpMethod.Post
        request.set_headers(self.json_format.build_http_headers())
        response = self.execute_request_direct(request)
        payload = response.json()
        if self.json_format.metadata == ODataMetadataLevel.Verbose:
            payload = payload['d']['GetContextWebInformation']
        self.contextWebInformation = ContextWebInformation()
        self.contextWebInformation.from_json(payload)

    def execute_query(self):
        self.pending_request.before_execute_request(self._build_specific_query)
        super(ClientContext, self).execute_query()

    def _build_specific_query(self, request, query):
        if request.method == HttpMethod.Post:
            self.ensure_form_digest(request)
        # set custom SharePoint control headers
        if isinstance(self.json_format, JsonLightFormat):
            if isinstance(query, DeleteEntityQuery):
                request.set_header("X-HTTP-Method", "DELETE")
                request.set_header("IF-MATCH", '*')
            elif isinstance(query, UpdateEntityQuery):
                request.set_header("X-HTTP-Method", "MERGE")
                request.set_header("IF-MATCH", '*')

    @property
    def web(self):
        """Get Web client object"""
        if not self.__web:
            self.__web = Web(self)
        return self.__web

    @property
    def site(self):
        """Get Site client object"""
        if not self.__site:
            self.__site = Site(self)
        return self.__site
