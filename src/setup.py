from distutils.core import setup

setup(
    name="Home Automation Hub",
    version="1.0",
    description="Home Automation Hub",
    author="Cameron Gray",
    author_email="development@camerongray.me",
    url="https://github.com/camerongray1515",
    install_requires=[
        "paho-mqtt==1.1",
        "flask==0.12.2",
        "redis==2.10.3",
        "websockets==5.0.1",
        "aioredis==1.1.0",
        "gevent",
    ],
    packages=["home_automation_hub"],
    entry_points={
        "console_scripts": [
            ["home-automation-hub=home_automation_hub.main:main"]
        ]
    },
)
