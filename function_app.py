from openai import OpenAI
import azure.functions as func
import logging
import openai

secret_key = ""

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="firstfunctionapi")
def firstfunctionapi(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="completionAPI", auth_level=func.AuthLevel.ANONYMOUS)
def completionAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    client = OpenAI(
        api_key=secret_key,
    )

    req_body = req.get_json()

    completion = client.chat.completions.create(
        model=req_body["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req_body["prompt"]}
        ],
        max_tokens=req_body["max_tokens"],
        temperature=req_body["temperature"],
    )

    return func.HttpResponse(completion.choices[0].message.content, status_code=200)

@app.route(route="imageAPI", auth_level=func.AuthLevel.ANONYMOUS)
def imageAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function for image generation processed a request.')

    try:
        # Get the request body
        req_body = req.get_json()

        # Set up OpenAI client
        client = OpenAI(api_key=secret_key)  # Replace with your OpenAI API key

        # Extract model, prompt, and other parameters from the request
        model = req_body.get("model", "dall-e-3")  # Default to "dall-e-3"
        prompt = req_body.get("prompt", "a white siamese cat")  # Default prompt
        size = req_body.get("size", "1024x1024")  # Default size
        n = req_body.get("n", 1)  # Default to generating one image
        quality = req_body.get("quality", "standard")  # Default quality

        # Generate image based on the provided parameters
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
        )

        # Get the URL of the generated image
        image_url = response.data[0].url

        # Return the image URL as the response
        return func.HttpResponse(image_url, status_code=200)

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return func.HttpResponse(f"Error generating image: {str(e)}", status_code=500)