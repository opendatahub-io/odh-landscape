# Installation

## Prerequisites

First we need to install node and have the project downloaded

### Install on Mac

1. Install [Homebrew](https://brew.sh/)
2. `brew install node`
3. `git clone git@github.com:opendatahub-io/odh-landscape.git`

### Install on Linux

1. `git clone git@github.com:opendatahub-io/odh-landscape.git`
2. Please follow [this script](https://github.com/cncf/landscapeapp/blob/master/update_server/setup.template) to install correct versions of `nodejs` and other packages on Linux.

## Development

(Before recreating those steps, please follow the instructions to clone the [landscape project](https://github.com/cncf/landscapeapp))[1]

1. Create a .env.local file to and override the environment variables that you want to use.
2. Run `make install` (Install the dependencies and download the modified landscape project).
3. Run `make import` (import the data of the csv into `landscape.yml`).
4. Run `make build` (Build a new instance of the app).
5. Run `make dev` (Launches a local verision).

[1]Right now, as the upstream project is very opinionated about the stack and their toolchain, the only method available to generate a new landscape is cloning the main project and executing the build targeting our landscape, as stated [here](https://github.com/cncf/landscapeapp/issues/711). The steps to download the project are:

1. Clone the landscape project `git clone https://github.com/opendatahub-io/landscapeapp`
2. Place the project in the same base folder as this project, the result should be the following:

```bash
> ls

odh-landscape landscapeapp
```

## Steps to fix/change features

This repository uses [our modified landscapeapp](https://github.com/opendatahub-io/landscapeapp) to build and deploy the webapp. Most of the logic of the app resides there. Running `make dev` ensures hot reloading when changing the project.

## Updating data

We use the `landscape.csv` file to update our database. Then with `make import` we call `tools/import_landscape.js` to generate `landscape.yml`. This file will be used by the landscapeapp to generate the `processed_landscape.yml` and the data stored in the app.

## Deployment

After building a new version, you must follow this steps to deploy a new version to [the main webpage](https://opendatahub.io/).

1. Clone the [ODH Webpage Repo](https://github.com/opendatahub-io/opendatahub.io).
2. Build a new version of the odh-landscape app.
3. Copy the contents of the `build/` folder into the `landscape/` folder in the opendatahub.io project.
4. Ensure everythin is working running `bundle exec jekyll serve` in the opendatahub.io project.