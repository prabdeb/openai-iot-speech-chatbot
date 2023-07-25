from setuptools import setup, find_packages

setup(
    name='OpenAI IoT Skill',
    description='OpenAI IoT Skills for Raspberry Pi 4',
    long_description="This is a demonstration of how to use OpenAI's GPT-3 to create several custom skills for IoT devices. Where the IoT device is a Raspberry Pi 4 with a microphone and speaker.",
    keywords='openai, gpt3, raspberry pi, iot, skills',
    url="https://github.com/prabdeb/openai-iot-speech-chatbot",
    author='Prabal Deb',
    author_email='prbldeb@gmail.com',
    license='MIT',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['openai_iot/gptskills/prompts/*.txt']},
    install_requires=[line.strip() for line in open('gptskills_requirements.txt')] + [line.strip() for line in open('orchestrator_requirements.txt')],
)
