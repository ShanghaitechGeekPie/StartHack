import joblib
res = joblib.load("meva_output.pkl")
humanpose = {}
for person in res.keys():
    sres = res[person]
    print(sres.keys())
    print(sres['pred_cam'].shape)
    print(sres['orig_cam'].shape)
    print(sres['verts'].shape)
    print(sres['pose'].shape)
    print(len(sres["joints3d"][0]))
    for i in range(len(sres["frame_ids"])):
        d = {}
        for x in list(sres.keys()):
            if sres[x] is not None:
                d[x] = sres[x][i]
        humanpose[sres["frame_ids"][i]] = d

#for x in humanpose.keys():
#    print(len(humanpose[x]['verts']))
    

