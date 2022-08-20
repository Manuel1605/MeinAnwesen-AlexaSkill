# "Mein Anwesen" Skill

An alexa skill (German only) to manage properties in your private house.

Functionality supported:
- "Alexa, frag mein Anwesen nach der Pool Temperatur".



This project was started with the motivation to explore Amazon Alexa and AWS IoT Core.
It is not plug-and-play. You need to buy hardware and put it together on your own.
I used the following components:
1. Raspberry Pi 4 Model B
2. DS18B20 waterproof temperature sensor
4. 4,7k Resistor


## How to build the project
### Alexa Skill
You have to create an Amazon Developer Account and start a new skill.
I called mine "Mein Anwesen". The backend will handle all default intents and one custom Intent `SwimmingPoolTemperatureIntentHandler` which returns the captured temperature value.

### Alexa backend
This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- alexa/ragglach17-skill-function - Code for the application's Lambda function.
- alexa/template.yaml - A template that defines the application's AWS resources. **IMPORTANT: Please replace the skill id with your own one in this file.**

The application uses several AWS resources, including a Lambda function and dynamoDB. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

#### Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Node.js - [Install Node.js 10](https://nodejs.org/en/), including the NPM package management tool.
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
alexa$ sam build
alexa$ sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

#### Use the SAM CLI to build and test locally

Build your application with the `sam build` command.

```bash

alexa$ sam build
```

The SAM CLI installs dependencies defined in `alexa/ragglach17-skill-function/package.json`, creates a deployment package, and saves it in the `alexa/.aws-sam/build` folder.

#### Connect the backend to the alexa skill.
In the Amazon Developer Console you need to insert the Amazon Resource Name (ARN) of the lambda function as target.
### IoT Backend
The AWS IoT Core Resources are defined as Cloudformation template. Run the following command to create a Stack.
```
aws cloudformation create-stack \
   --stack-name mein-anwesen \
   --template-body file://<path-to-project>/iot/infrastructure/iot-core.yaml
```

In order to put the hardware together I recommend the following manual:
[https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/)


There is no automated process to manage the IoT Device and the required software. Roughly you need to execute the following steps:  
- Go to AWS Web Console and download the IoT Certificates.
- These need to be placed in `iot/pool-temperature-sensor/certificates`
- Specify the right certificate paths in `iot/pool-temperature-sensor/main.py`
- Transmit the `iot/pool-temperature-sensor` folder to the Raspberry Pi.
- Run `pool-temperature-sensor$ pip3 install -r requirements.txt` on the Raspberry PI
- `pool-temperature-sensor$ python3 main.py` starts the application.

The last command pushes the temperature value via AWS IoT Core to a dynamoDB table. I installed a cronjob on the device to push every 15 minutes.


Depending on your Skill Definition you should now ask Alexa a question which triggers the `SwimmingPoolTemperatureIntent`. It should tell you the last captured temperature.

