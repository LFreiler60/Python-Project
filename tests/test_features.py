import pytest

from ml.features import flight_category

#parametrize allows for all scenarios to be tested
@pytest.mark.parametrize(
	"ceiling_ft, visibility_sm, expected",
	[
		(5000, 10, "VFR"),
		(2500, 10, "MVFR"),
		(5000, 4, "MVFR"),
       	(800, 10, "IFR"),
        (5000, 2, "IFR"),
		(400, 10, "LIFR"),
        (5000, 0.5, "LIFR"),
        ],
)

def test_flight_category(
	ceiling_ft,
	visibility_sm,
	expected,
):
	result = flight_category(
		ceiling_ft,
		visibility_sm,
	)
	#does the expected match the actual function result
	assert result == expected 
	
		
