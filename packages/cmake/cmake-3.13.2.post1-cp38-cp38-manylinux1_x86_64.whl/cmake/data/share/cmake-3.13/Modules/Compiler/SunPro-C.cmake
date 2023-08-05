# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

include(Compiler/SunPro)

set(CMAKE_C_VERBOSE_FLAG "-#")

set(CMAKE_C_COMPILE_OPTIONS_PIC -KPIC)
set(CMAKE_SHARED_LIBRARY_C_FLAGS "-KPIC")
set(CMAKE_SHARED_LIBRARY_CREATE_C_FLAGS "-G")
set(CMAKE_SHARED_LIBRARY_RUNTIME_C_FLAG "-R")
set(CMAKE_SHARED_LIBRARY_RUNTIME_C_FLAG_SEP ":")
set(CMAKE_SHARED_LIBRARY_SONAME_C_FLAG "-h")

string(APPEND CMAKE_C_FLAGS_INIT " ")
string(APPEND CMAKE_C_FLAGS_DEBUG_INIT " -g")
string(APPEND CMAKE_C_FLAGS_MINSIZEREL_INIT " -xO2 -xspace -DNDEBUG")
string(APPEND CMAKE_C_FLAGS_RELEASE_INIT " -xO3 -DNDEBUG")
string(APPEND CMAKE_C_FLAGS_RELWITHDEBINFO_INIT " -g -xO2 -DNDEBUG")

set(CMAKE_DEPFILE_FLAGS_C "-xMD -xMF <DEPFILE>")

# Initialize C link type selection flags.  These flags are used when
# building a shared library, shared module, or executable that links
# to other libraries to select whether to use the static or shared
# versions of the libraries.
foreach(type SHARED_LIBRARY SHARED_MODULE EXE)
  set(CMAKE_${type}_LINK_STATIC_C_FLAGS "-Bstatic")
  set(CMAKE_${type}_LINK_DYNAMIC_C_FLAGS "-Bdynamic")
endforeach()

set(CMAKE_C_LINKER_WRAPPER_FLAG "-Qoption" "ld" " ")
set(CMAKE_C_LINKER_WRAPPER_FLAG_SEP ",")

if (CMAKE_C_COMPILER_VERSION VERSION_GREATER_EQUAL 5.13)
  set(CMAKE_C90_STANDARD_COMPILE_OPTION "-std=c89")
  set(CMAKE_C90_EXTENSION_COMPILE_OPTION "-std=c89")
  set(CMAKE_C99_STANDARD_COMPILE_OPTION "-std=c99")
  set(CMAKE_C99_EXTENSION_COMPILE_OPTION "-std=c99")
  set(CMAKE_C11_STANDARD_COMPILE_OPTION "-std=c11")
  set(CMAKE_C11_EXTENSION_COMPILE_OPTION "-std=c11")
elseif (CMAKE_C_COMPILER_VERSION VERSION_GREATER_EQUAL 5.11)
  set(CMAKE_C90_STANDARD_COMPILE_OPTION "")
  set(CMAKE_C90_EXTENSION_COMPILE_OPTION "")
  set(CMAKE_C99_STANDARD_COMPILE_OPTION "-xc99")
  set(CMAKE_C99_EXTENSION_COMPILE_OPTION "-xc99")
endif()

__compiler_check_default_language_standard(C 5.11 90 5.14 11)

set(CMAKE_C_CREATE_PREPROCESSED_SOURCE "<CMAKE_C_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -E <SOURCE> > <PREPROCESSED_SOURCE>")
set(CMAKE_C_CREATE_ASSEMBLY_SOURCE "<CMAKE_C_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -S <SOURCE> -o <ASSEMBLY_SOURCE>")
