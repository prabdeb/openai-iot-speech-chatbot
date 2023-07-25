build-copy-files:
	cp -r ../azure_iot_solution/modules/gptskills/requirements.txt ./gptskills_requirements.txt
	cp -r ../azure_iot_solution/modules/orchestrator/requirements.txt ./orchestrator_requirements.txt
	python3 ./utils_copy_files.py copy

build-wheel-package: build-copy-files
	python3 setup.py bdist_wheel

build-wheel-package-clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./openai_iot.egg-info
	rm -rf ./gptskills_requirements.txt
	rm -rf ./orchestrator_requirements.txt
	python3 ./utils_copy_files.py delete

build: build-wheel-package-clean build-wheel-package

clean: build-wheel-package-clean

install: build-wheel-package
	pip3 install ./dist/OpenAI_IoT_Skill-1.1-py3-none-any.whl

install-force: build-wheel-package
	pip3 install ./dist/OpenAI_IoT_Skill-1.1-py3-none-any.whl --force-reinstall
