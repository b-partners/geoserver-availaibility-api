FROM public.ecr.aws/lambda/python:3.12

COPY __init__.py app.py address_converter.py check_availability.py data.json tile_downloader.py requirements.txt ./

RUN python3.12 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
