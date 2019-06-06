import scolp

scolp_cfg = scolp.Config()
scolp_cfg.add_columns("country", "population (mil)", "capital city", "life expectancy (female)",
                      "life expectancy (male)", "fertility rate")
scolper = scolp.Scolp(scolp_cfg)
scolper.print("Netherlands", 16.81, "Amsterdam", 83, 79, 1.5,
              "China", 1350.0, "Beijing", 76, 72, 1.8,
              "Israel", 7.71, "Jerusalem", 84, 80, 2.7,
              "Nigeria")
scolper.print(174.51)