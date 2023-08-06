# Empyrion Build Assistant
 ## What is this?
 This is a python package that I created to automate a lot of the tasks that go into building mods for Empyrion. 
 ## How do I use it?
 assuming you have python 3.8 installed,the package is loaded using:
 ```shell script
pip install empyrionbuildassistant
``` 

Once installed, you an view the help using:
```
python -m EmpyrionBuildAssistant -h
```

which should show:

```text
usage: __main__.py [-h] [--copyDllsToFolder COPYDLLSTOFOLDER] [--modName MODNAME] [--bundleAndDeployMod BUNDLEANDDEPLOYMOD] [-clearLogs] [-watchLogs] [-launchServer]

scripts to help build and deploy empyrion mods

optional arguments:
  -h, --help            show this help message and exit
  --copyDllsToFolder COPYDLLSTOFOLDER
                        the folder to copied the required dlls to
  --modName MODNAME     the name of the mod being deployed
  --bundleAndDeployMod BUNDLEANDDEPLOYMOD
                        the folder containing the mod that will be deployed
  -clearLogs            clears the logs on the dedi server
  -watchLogs            watches the dedi server logs, press enter to exit
  -launchServer         launches the dedi server, press enter to kill

Note: modname must be specified when using the bundleAndDeployMod option
```

## Can the commands be chained?

Yup, the most useful command that I use for debugging is

```shell script
python -m EmpyrionBuildAssistant -clearLogs -watchLogs -launchServer
```

Which clears the logs launches the server and creates a window that watches all of the changes to the server's log files.  When you press enter, it will terminate the server process (and its children)

## How does it work?

It starts by scanning your windows registry (sorry at the moment this works on windows only :( ) to locate your steam installation path.  From there it traverses the steamapps manifests to locate the install location of the dedicated server (Steam AppID 530870) and it uses that path as the root for all of the commands.

## Is this like, "done"?

HAHAHAHAHAHAHAHAAHAHAHAHAHA

No, it is not, as evidence I present the complete absence of tests.  this is really just a collection of scripts that I threw together to make another problem that I'm working on easier to solve.

If you'd like to help please leave issues or PRs

## What about the obvious question you haven't addressed here?

If you have a question I didn't think of, feel free to leave it as an issue.  If it gets asked a lot (or it seems like a really good question) I'll add it here.
