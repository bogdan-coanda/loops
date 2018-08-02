import photos

albumAssetCollection = photos.create_album('k02s0.grown')

frameAssets = []
for index in range(139):
	frameAssets.append(photos.create_image_asset('frames/frame.'+'{:0>3}'.format(index)+'.png'))
	
albumAssetCollection.add_assets(frameAssets)
	
