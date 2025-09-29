FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY __init__.py app.py address_converter.py check_availability.py tile_downloader.py data.json layer-list.json requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt -t ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]
