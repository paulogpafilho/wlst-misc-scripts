# Weblogic WLST Miscellaneous Scripts

This is a repository of miscellaneous WLST scripts.

Scripts are examples on how to implement several tasks related to WLS monitoring, admin and configuration.

## Getting Started

Read the script comments for each description and requirements but as a general rule, scripts will be used by invoking WLST and passing the script as argument.

For example:

/home/oracle/MW_HOME/common/bin/wlst.sh SCRIPT_NAME

Some scripts will require additional files; others some environment variable to be set.

Additional required files will be provided with the script and the environment variable, if any, will be described in the script comments.

### Prerequisites

A valid Weblogic Server installation and/or additional Fusion Middleware components.

### Installing

Just copy the desired script and the additional required files to a folder and invoke WLST passing the script as argument.

For example:

```
/home/oracle/MW_HOME/common/bin/wlst.sh create_users.py
```

## Authors

* **Paulo Albuquerque** - [LinkedIn](https://www.linkedin.com/in/paulogpafilho/)

## License

This project/code is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
