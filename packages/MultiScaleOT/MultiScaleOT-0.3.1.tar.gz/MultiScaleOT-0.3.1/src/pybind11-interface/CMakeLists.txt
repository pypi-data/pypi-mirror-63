if( USE_PYBIND )

	add_library(pybind11-interface SHARED MultiScaleOT-pybind11-interface.cpp)

	target_compile_options(pybind11-interface PUBLIC ${PYBIND_COMPILE_OPTIONS})
	
	target_link_libraries(pybind11-interface
		Common
		)
		
	if ( USE_SINKHORN )
		target_link_libraries(pybind11-interface
			Sinkhorn
			)
	endif ( USE_SINKHORN)
	
	set_target_properties(pybind11-interface PROPERTIES PREFIX "")
	set_target_properties(pybind11-interface PROPERTIES SUFFIX ${PYTHON_EXTENSION_SUFFIX})
	set_target_properties(pybind11-interface PROPERTIES OUTPUT_NAME MultiScaleOT)

	install (TARGETS pybind11-interface DESTINATION ${CMAKE_BINARY_DIR}/../python)


endif( USE_PYBIND )
