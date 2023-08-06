from routing.controllers.response.custom_response import CustomResponse

class HealthController:

    def on_get(self, req, resp: CustomResponse):
        resp.message = 'Peticion Exitosa.'
        resp.data_response = {'alive': True}
