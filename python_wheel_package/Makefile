build-copy-files:
	cp -r ../azure_iot_solution/module/gpt-skills/requirements.txt ./gpt-skills_requirements.txt
	cp -r ../azure_iot_solution/module/orchestrator/requirements.txt ./orchestrator_requirements.txt
	python3 ./utils_copy_files.py copy

build-wheel-package: build-copy-files
	python3 setup.py bdist_wheel

build-wheel-package-clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./openai_iot.egg-info
	rm -rf ./gpt-skills_requirements.txt
	rm -rf ./orchestrator_requirements.txt
	python3 ./utils_copy_files.py delete

build: build-wheel-package-clean build-wheel-package

clean: build-wheel-package-clean

install: build-wheel-package
	pip3 install ./dist/openai_iot-0.0.1-py3-none-any.whl
