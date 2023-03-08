	nios_project u0 (
		.clk_clk                                            (<connected-to-clk_clk>),                                            //                                  clk.clk
		.reset_reset_n                                      (<connected-to-reset_reset_n>),                                      //                                reset.reset_n
		.button_external_connection_export                  (<connected-to-button_external_connection_export>),                  //           button_external_connection.export
		.accelerometer_spi_external_interface_I2C_SDAT      (<connected-to-accelerometer_spi_external_interface_I2C_SDAT>),      // accelerometer_spi_external_interface.I2C_SDAT
		.accelerometer_spi_external_interface_I2C_SCLK      (<connected-to-accelerometer_spi_external_interface_I2C_SCLK>),      //                                     .I2C_SCLK
		.accelerometer_spi_external_interface_G_SENSOR_CS_N (<connected-to-accelerometer_spi_external_interface_G_SENSOR_CS_N>), //                                     .G_SENSOR_CS_N
		.accelerometer_spi_external_interface_G_SENSOR_INT  (<connected-to-accelerometer_spi_external_interface_G_SENSOR_INT>)   //                                     .G_SENSOR_INT
	);

