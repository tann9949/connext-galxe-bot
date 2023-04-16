FROM public.ecr.aws/lambda/python:3.9

RUN yum install -y gcc

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY src ${LAMBDA_TASK_ROOT}/src
COPY lambda_transfers.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_transfers.lambda_handler"]