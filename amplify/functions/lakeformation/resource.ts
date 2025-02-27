import { execSync } from "node:child_process";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { defineFunction } from "@aws-amplify/backend";
import { DockerImage, Duration } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import fs from 'fs-extra';

const functionDir = path.dirname(fileURLToPath(import.meta.url));

export const lakeformationFunctionHandler = defineFunction(
    (scope) =>
        new Function(scope, "lakeformation", {
            handler: "index.handler",
            runtime: Runtime.PYTHON_3_12, // or any other python version
            timeout: Duration.seconds(20), //  default is 3 seconds
            code: Code.fromAsset(functionDir, {
                bundling: {
                    image: DockerImage.fromRegistry("dummy"), // replace with desired image from AWS ECR Public Gallery
                    local: {
                        tryBundle(outputDir: string) {
                            execSync(
                                `python -m pip install -r ${path.join(functionDir, "requirements.txt")} -t ${path.join(outputDir)} --platform manylinux2014_x86_64 --only-binary=:all:`
                            );
                            fs.copySync(functionDir, outputDir);
                            return true;
                        },
                    },
                },
            }),
        })
);