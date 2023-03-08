	component nios_project is
		port (
			clk_clk                                            : in    std_logic                    := 'X';             -- clk
			reset_reset_n                                      : in    std_logic                    := 'X';             -- reset_n
			button_external_connection_export                  : in    std_logic_vector(1 downto 0) := (others => 'X'); -- export
			accelerometer_spi_external_interface_I2C_SDAT      : inout std_logic                    := 'X';             -- I2C_SDAT
			accelerometer_spi_external_interface_I2C_SCLK      : out   std_logic;                                       -- I2C_SCLK
			accelerometer_spi_external_interface_G_SENSOR_CS_N : out   std_logic;                                       -- G_SENSOR_CS_N
			accelerometer_spi_external_interface_G_SENSOR_INT  : in    std_logic                    := 'X'              -- G_SENSOR_INT
		);
	end component nios_project;

	u0 : component nios_project
		port map (
			clk_clk                                            => CONNECTED_TO_clk_clk,                                            --                                  clk.clk
			reset_reset_n                                      => CONNECTED_TO_reset_reset_n,                                      --                                reset.reset_n
			button_external_connection_export                  => CONNECTED_TO_button_external_connection_export,                  --           button_external_connection.export
			accelerometer_spi_external_interface_I2C_SDAT      => CONNECTED_TO_accelerometer_spi_external_interface_I2C_SDAT,      -- accelerometer_spi_external_interface.I2C_SDAT
			accelerometer_spi_external_interface_I2C_SCLK      => CONNECTED_TO_accelerometer_spi_external_interface_I2C_SCLK,      --                                     .I2C_SCLK
			accelerometer_spi_external_interface_G_SENSOR_CS_N => CONNECTED_TO_accelerometer_spi_external_interface_G_SENSOR_CS_N, --                                     .G_SENSOR_CS_N
			accelerometer_spi_external_interface_G_SENSOR_INT  => CONNECTED_TO_accelerometer_spi_external_interface_G_SENSOR_INT   --                                     .G_SENSOR_INT
		);

