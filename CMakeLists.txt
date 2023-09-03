cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(LING_Registration)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/LING_Registration")
set(EXTENSION_CATEGORY "3D US Liver")
set(EXTENSION_CONTRIBUTORS "Shuwei Xing (Robarts Research Institute)")
set(EXTENSION_DESCRIPTION "This is an extension to achieve the real-time alignment of tracked 2D US with pre-operative CT/MRI.")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/LING_Registration.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/LING_Registration/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(ReadSequentialData)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
