# TraVersion
TraVersion is similar way of maintaining semantic versioning in python, where the major points are introduced in this repository.

**Usage Example:**
* Default version
    ```python
    from traVer import Version
    version = Version()
    
    # Default version will be 1.0.0
    print(version)
    ```
  _Output:_
    ```bash
    >> 1.0.0
    ```
* Assigning version
    ```python
    from traVer import Version
    version = Version("2.3.4-beta.5")
    
    # You can specify major, minor, patch, preRelName, preRelease
    print(version.major)
    print(version.patch)
    ```
    _Output:_
    ```bash
    >> 2
    4
  ```
**Note:**

   Anyone interested to contribute code or give some ideas to improve the versions to this repository are most welcome. 
    
**Do you know?**
    
   > _The word TraVersion is taken from Traverse which means  "to go or travel across or over"_
