# Environment06 Revision01 — review issues

|Issue|Status|Next action|
|---|---|---|
|Excessive large-clump blanket|Reduced; visual approval pending|84,204→22,914 native instances;199 coarse filler chunks disabled. Review before accepting the lower density.|
|Artificial ground / repeating surface|Partially improved, still outstanding|Continuous opaque painted turf replaces smooth ground in dominant grass layers; broad uniformity, olive tint and repeating strokes remain visible. Judge at player height.|
|Rendering cost|Measured reduction, still expensive|Six matched Editor views show lower PlayerLoop/render-thread/GPU counters and submissions. Standalone performance not remeasured.|
|Short grass / close cards|Candidate limitation|18-triangle cropped blade strips are lightweight; close shapes and culling remain noticeable. No custom grass framework deployed.|
|Flower density / older bushes|Manual composition review pending|Fewer colonies replace speckled coverage; confirm sparseness and retained large clumps are appropriate.|
|Road edge transition|Outstanding|Underlying Terrain wear improved, but hard road-mesh outline remains. No geometry/road material change authorized in this pass.|
|Historical NullReference|Traced to Editor window maximization; not reproduced|No project/gameplay stack in captured trace. Capture a new full trace if it returns. No speculative fix.|
|Normal-input locomotion/orbit validation|Passed focused Play-mode input test|12waypoints;207/207grounded samples; Idle/Walk/Sprint, stopping and91.96°orbit verified. Automated input path, not manual comfort approval.|
|Protected settings incl UnityConnect|Retained unchanged; previous approval pending|All five hashes identical. No normalization/revert/services change.|

See README.md for evidence and limitations. No artistic approval implied by test counts.
