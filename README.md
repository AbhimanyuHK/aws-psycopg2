psycopg2 Python Library for AWS Lambda
======================================

This is a custom compiled psycopg2 C library for Python. Due to AWS Lambda
missing the required PostgreSQL libraries in the AMI image, we needed to
compile psycopg2 with the PostgreSQL `libpq.so` library statically linked
libpq library instead of the default dynamic link.


### Install and setup

``` pip install aws-psycopg2 ```

### Source code : https://github.com/AbhimanyuHK/aws-psycopg2 

### Instructions on compiling this package from scratch

Here was the process that was used to build this package. You will need to
perform these steps if you want to build a newer version of the psycopg2
library.

1. Download the
  [PostgreSQL source code](https://ftp.postgresql.org/pub/source/v9.4.3/postgresql-9.4.3.tar.gz) and extract into a directory.
2. Download the
  [psycopg2 source code](http://initd.org/psycopg/tarballs/PSYCOPG-2-6/psycopg2-2.6.1.tar.gz) and extract into a directory.
3. Go into the PostgreSQL source directory and execute the following commands:
  - `./configure --prefix {path_to_postgresql_source} --without-readline --without-zlib`
  - `make`
  - `make install`
4. Go into the psycopg2 source directory and edit the `setup.cfg` file with the following:
  - `pg_config={path_to_postgresql_source/bin/pg_config}`
  - `static_libpq=1`
5. Execute `python setup.py build` in the psycopg2 source directory.

After the above steps have been completed you will then have a build directory
and the custom compiled psycopg2 library will be contained within it. Copy this
directory into your AWS Lambda package and you will now be able to access
PostgreSQL from within AWS Lambda using the psycopg2 library.


## Project Status

> **Status: Maintenance / Development Paused**

This project was originally created to provide a custom `psycopg2` package for AWS Lambda by compiling PostgreSQL `libpq` and statically linking it with `psycopg2`. At the time, this approach addressed compatibility limitations when deploying PostgreSQL-based Python applications to AWS Lambda.

### Why development is currently paused

The AWS Lambda and Python ecosystem has evolved significantly since this project was created.

Modern versions of `psycopg2-binary` provide pre-built packages that bundle the required PostgreSQL client libraries, including `libpq`. Psycopg 3 also provides binary distributions that simplify deployment without requiring users to manually compile PostgreSQL client libraries.

As a result, the original custom compilation approach used by this project is no longer necessary for most AWS Lambda use cases.

The original workflow:

```text
PostgreSQL Source
       ↓
Compile libpq
       ↓
Compile psycopg2
       ↓
Static linking
       ↓
Create Lambda ZIP
       ↓
AWS Lambda Layer
```

can now generally be replaced with modern binary distributions:

```text
psycopg2-binary / psycopg[binary]
             ↓
      Lambda-compatible
       packaging/build
             ↓
        ZIP / Layer
             ↓
        AWS Lambda
```

### Project decision

Development of the original custom `aws-psycopg2` implementation is therefore **paused** rather than continuing to maintain an increasingly complex custom PostgreSQL/`libpq` build process.

This repository is retained for:

* Historical reference
* Understanding native Python dependencies in AWS Lambda
* Understanding PostgreSQL `libpq` and `psycopg2` compilation
* Reference for creating Lambda layers containing native dependencies
* Potential future work around cross-platform Lambda dependency packaging

### Future direction

If development resumes, the project will likely be redesigned as a **cross-platform AWS Lambda native dependency builder**, rather than maintaining a custom fork of `psycopg2`.

Potential future capabilities could include:

* Python 3.12+
* Amazon Linux 2023 compatibility
* x86_64 and ARM64 builds
* Automated GitHub Actions builds
* Docker-based reproducible builds
* Lambda Layer ZIP generation
* Native dependency validation
* Support for multiple Python packages with native binaries

### Community Feedback

If you are still using this project or believe that a custom `aws-psycopg2` package is still required for a specific AWS Lambda use case, **feel free to create an issue** and describe your requirements or compatibility problem.

Community feedback and real-world use cases may help determine whether development should be resumed or whether the project should evolve into a broader AWS Lambda native dependency builder.

Thank you to everyone who has used, contributed to, or provided feedback on this project.
