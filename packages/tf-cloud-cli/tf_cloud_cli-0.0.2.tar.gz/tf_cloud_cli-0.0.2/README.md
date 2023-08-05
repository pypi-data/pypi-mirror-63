# TF Cloud CLI

A simple CLI for interacting with the Terraform Cloud API.

Currently only supports listing organizations, workspaces and updating the run mode for workspaces

## Install

```
pip install tf-cloud-cli
```

### Token Setup

Get an API token from the Terraform cloud app.

Token can either be set in an environment variable called `TF_TOKEN` or in a file named `.credentials.conf`


## Usage

```
tf_cloud_cli --help                                                                                                                                                                                         <aws:sensurance>
Usage: tf_cloud_cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list-organizations
  organization
```

### List Organizations

```
tf_cloud_cli list-organizations
```

### List Workspaces

```
tf_cloud_cli organization -o MyOrganization list-workspaces
```

### Show workspace details

```
tf_cloud_cli organization -o MyOrganization workspace -w my-workspace show
```

### Set local execution for workspace

```
tf_cloud_cli organization -o MyOrganization workspace -w my-workspace set-local-execution
```