from setuptools import setup, find_packages

setup(
    name='OpenAI IoT Skill',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['openai_iot/gptskills/prompts/*.txt']},
    install_requires=[line.strip() for line in open('gptskills_requirements.txt')] + [line.strip() for line in open('orchestrator_requirements.txt')],
)
