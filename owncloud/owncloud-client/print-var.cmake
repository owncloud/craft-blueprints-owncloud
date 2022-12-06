if(NOT TARGET_SCRIPT OR NOT TARGET_VAR)
    message(FATAL_ERROR "Required variable(s) not defined")
endif()

include(${TARGET_SCRIPT})
execute_process(COMMAND ${CMAKE_COMMAND} -E echo "${${TARGET_VAR}}")
