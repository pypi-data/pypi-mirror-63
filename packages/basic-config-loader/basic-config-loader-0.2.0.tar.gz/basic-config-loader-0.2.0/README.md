# basic-config-loader

Load a JSON configuration from a file, or from multiple folders on the filesystem.

## Getting Started

### Prerequisites

This project has no dependencies. Yay!

### Installing

```
pip install basic-config-loader
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Usage

```
import configLoader as cl
...
CONFIG = cl.loadConfig(...)
...
```    
:param path: the path to look for the file. It is recommended to provide the result of os.path.join() rather than a manually typed path because a certain OS which must not be named has different path conventions than everyone else.

:param default: the configuration to return if loading from the filesystem fails.
    
:param fromHome: if True, look from the current user's home directory. If False, look from the root directory.
    
:param topSearchPath: if None, only look in the specified path for the file. Otherwise, a path should be provided. 'HOME' can be filled in as a shortcut for os.environ['HOME']. The exact behavior depends on fullSearchAlways.

:param fullSearchAlways: if False, and the directory specified in path is empty, move up one folder, up to topSearchPath, until a config file is found, and use the first file found. If no file is found, use the default config. If True, start with the default configuration and apply any changes from topSearchPath to path in order.

:return: the configuration if loading was successful, or the default configuration if loading failed.
