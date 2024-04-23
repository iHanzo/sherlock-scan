class LogPostRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the request is a POST request
        if request.method == 'POST':
            # Print request details
            print(f"Received POST request at {request.path}")
            print(f"POST data: {request.POST}")
            print(f"Headers: {dict(request.headers)}")

        return response
