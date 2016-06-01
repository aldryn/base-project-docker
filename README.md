# aldryn/base-project

[![](https://badge.imagelayers.io/aldryn/base-project.svg)](https://imagelayers.io/?images=aldryn/base-project:latest)

## Release process
Update changelog and bump version: the new version should follow the [aldryn/base](https://github.com/aldryncore/base-docker) image:

```
aldryn/base:3.2.0 => aldryn/base-project:3.2.0
```

If you need to do a seperate release without upgrading the baseproject, change the patch version:

```
aldryn/base-project:3.2.1
```

Once you go back to the next version of the base image, bump major/minor and reset patch to zero again:

```
aldryn/base:3.3.0 => aldryn/base-project:3.3.0
```
