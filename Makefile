DESCRIPTION?=Sample Bottle-Lambda application

ACCOUNT_ID?=
ROLE?=
REGION_NAME?=us-east-1

ENV?=dev
FUNCTION_NAME?=py_bottle_test
FUNCTION_HANDLER?=sample_lambda.sample_handler
MEMORY_SIZE?=128
TIMEOUT?=60

FUNCTION_ARN=arn:aws:lambda:$(REGION_NAME):$(ACCOUNT_ID):function:$(FUNCTION_NAME)
ROLE_ARN=arn:aws:iam::$(ACCOUNT_ID):role/$(ROLE)
VERSION=$(shell python setup.py -V)


all:
	$(MAKE) clean
	$(MAKE) build publish


validate:
	$(if $(ACCOUNT_ID),,$(error ACCOUNT_ID is undefined))
	$(if $(ROLE),,$(error ROLE is undefined))
	$(if $(REGION_NAME),,$(error REGION_NAME is undefined))
	$(if $(ENV),,$(error ENV is undefined))
	$(if $(FUNCTION_NAME),,$(error FUNCTION_NAME is undefined))
	$(if $(FUNCTION_HANDLER),,$(error FUNCTION_HANDLER is undefined))


virtualenv:
	if [ ! -d venv ]; then virtualenv -p python3 venv; fi
	if [ ! -f venv/bin/pip ]; then venv/bin/pip install awscli; fi
	venv/bin/pip install --upgrade -r requirements.txt


build: virtualenv
	LC_ALL=en_US.UTF-8 venv/bin/python setup.py sdist --formats=gztar
	mkdir build
	cp sample_lambda.py build/ && cp -R -v mcmweb build/
	- cat requirements.txt | grep -v boto > build/requirements.txt && venv/bin/pip install --upgrade --no-compile -r build/requirements.txt -t build/
	cd build/ && zip -9 -x *.pyc -r ../dist/$(FUNCTION_NAME)-$(VERSION)-lambda.zip . && cd ..
	rm -rf build


publish: validate build
	venv/bin/aws lambda create-function \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN) \
		--runtime python3.6 \
		--role $(ROLE_ARN) \
		--handler "$(FUNCTION_HANDLER)" \
		--description "$(DESCRIPTION)" \
		--timeout $(TIMEOUT) \
		--memory-size $(MEMORY_SIZE) \
		--zip-file fileb://dist/$(FUNCTION_NAME)-$(VERSION)-lambda.zip
#	venv/bin/aws lambda add-permission \
#		--region $(REGION_NAME) \
#		--function-name $(FUNCTION_ARN) \
#		--source-arn $(EVENT_SOURCE_ARN) \
#		--principal events.amazonaws.com \
#		--action 'lambda:InvokeFunction' \
#		--statement-id '$(FUNCTION_NAME)'
#	venv/bin/aws events put-targets \
#		--region $(REGION_NAME) \
#		--rule $(EVENT_NAME) \
#		--targets '{"Id" : "1", "Arn": "$(FUNCTION_ARN)"}'


update: validate build
	venv/bin/aws lambda update-function-code \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN) \
		--zip-file fileb://dist/$(FUNCTION_NAME)-$(VERSION)-lambda.zip
	venv/bin/aws lambda publish-version \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN) \
		--description "Package $(FUNCTION_NAME) version $(VERSION)"


destroy: validate
	venv/bin/aws lambda delete-function \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN)


clean:
	rm -rf build/
	rm -f dist/*
