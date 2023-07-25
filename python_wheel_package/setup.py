from setuptools import setup, find_packages

setup(
    name='OpenAI IoT Skill',
    version='1.1',
    packages=find_packages(),
    install_requires=[line.strip() for line in open('gpt-skills_requirements.txt')] + [line.strip() for line in open('orchestrator_requirements.txt')],
)
