CEILING_COVERS = {"BKN", "OVC", "VV"}

#cloud_layers is a dictionary 
def extract_ceiling(cloud_layers):
	""""Return the lowest reported ceiling in feet AGL."""

	#checks if list is empty/missing meaning there are no ceilings
	if not cloud_layers:	
		return None
	
	#empty list to store ceilings
	ceiling_bases = [] 

	#gets values from dictionary
	for layer in cloud_layers:
			#is it bkn, ovc, vv, sct?
			cover = layer.get("cover")
			#gets altitude of base
			base = layer.get("base")

			#checks if the cover is a ceiling and if there is a reported alititude for ceiling
			#if so, adds that ceiling to list
			if cover in CEILING_COVERS and base is not None:
				ceiling_bases.append(base)

			if not ceiling_bases:
				return None
			
			#minimun is best for prediction model 
			return min(ceiling_bases)







def flight_category(ceiling_ft, visibility_sm):
	"""Classify fight conditions from ceiling and visiblity"."""

	if ceiling_ft < 500 or visibility_sm <1:
		return "LIFR"


	if ceiling_ft < 1000 or visibility_sm <3:
		return "IFR"
	
	if ceiling_ft <= 3000 or visibility_sm <=5:
		return "MVFR"

	return "VFR"
