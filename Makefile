DESCRIPTION=Elasticsearch cluster curator

ACCOUNT_ID?=444914307613
REGION_NAME?=us-east-1
ROLE?=lambda_varnish_dynamic_elb

ENV?=prod
#EVENT_NAME?=daily_event
FUNCTION_NAME?=py_bottle_test
MEMORY_SIZE=128
TIMEOUT?=60

#EVENT_SOURCE_ARN=arn:aws:events:$(REGION_NAME):$(ACCOUNT_ID):rule/$(EVENT_NAME)
#FUNCTION_ARN=arn:aws:lambda:$(REGION_NAME):$(ACCOUNT_ID):function:$(ENV)-$(FUNCTION_NAME)
FUNCTION_ARN=arn:aws:lambda:$(REGION_NAME):$(ACCOUNT_ID):function:$(FUNCTION_NAME)
ROLE_ARN=arn:aws:iam::$(ACCOUNT_ID):role/$(ROLE)
VERSION=$(shell python setup.py -V)

export


all:
	$(MAKE) clean
	$(MAKE) build publish


virtualenv:
	if [ ! -d venv ]; then virtualenv venv; venv/bin/pip install --upgrade awscli; fi
	venv/bin/pip install --upgrade -r requirements.txt


build: virtualenv
	LC_ALL=en_US.UTF-8 venv/bin/python setup.py sdist --formats=gztar
	mkdir build
	cp sample_lambda.py build/ && cp -R -v mcmweb build/
	- cat requirements.txt | grep -v boto > build/requirements.txt && venv/bin/pip install --upgrade --no-compile -r build/requirements.txt -t build/
	pushd build/ && zip -9 -r ../dist/$(FUNCTION_NAME)-$(VERSION)-lambda.zip . && popd
	rm -rf build


publish: build
	venv/bin/aws lambda create-function \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN) \
		--runtime python2.7 \
		--role $(ROLE_ARN) \
		--handler lambda.lambda_handler \
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


update: build
	venv/bin/aws lambda update-function-code \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN) \
		--zip-file fileb://dist/$(FUNCTION_NAME)-$(VERSION)-lambda.zip
	venv/bin/aws lambda publish-version \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN) \
		--description "Package $(FUNCTION_NAME) version $(VERSION)"


destroy:
	venv/bin/aws lambda delete-function \
		--region $(REGION_NAME) \
		--function-name $(FUNCTION_ARN)


clean:
	rm -rf build/
	rm -f dist/*
