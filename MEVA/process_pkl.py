import joblib
import numpy as np
res = joblib.load("Sout_meva_output.pkl")
for person in res.keys():
    sres = res[person]
    result = []
    print(len(sres["frame_ids"]))
    nw = 0
    for i in range(sres['frame_ids'][-1]):
        if sres["frame_ids"][nw + 1] == i:
            nw += 1
        if sres["frame_ids"][nw] != i:
            verts_delta = sres['verts'][nw + 1] - sres['verts'][nw]
            cam_delta = sres['pred_cam'][nw + 1] - sres['pred_cam'][nw]
            orig_cam_delta = sres['orig_cam'][nw + 1] - sres['orig_cam'][nw]
            percent = (i - sres['frame_ids'][nw]) / (sres['frame_ids'][nw + 1] - sres['frame_ids'][nw])
            result.append({
                'verts': sres['verts'][nw] + verts_delta * percent,
                'cam': sres['pred_cam'][nw] + cam_delta * percent,
                'orig_cam': sres['orig_cam'][nw] + orig_cam_delta * percent
            })
        else:
            result.append({
                'verts': sres['verts'][nw],
                'cam': sres['pred_cam'][nw],
                'orig_cam': sres['orig_cam'][nw]
            })
    joblib.dump(result, 'Sout_meva_output_dammit.pkl')