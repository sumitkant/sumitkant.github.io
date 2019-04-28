 // Build an array of points
 const segmentLength = 1;
 const nbrOfPoints = 10;
 const points = [];
 for (let i = 0; i < nbrOfPoints; i++) {
     points.push(i * segmentLength, 0, 0);
 }

 // Build the geometry
 const line = new MeshLine();
 line.setGeometry(points);
 const geometry = line.geometry;

 // Build the material with good parameters to animate it.
 const material = new MeshLineMaterial({
     transparent: true,
     lineWidth: 0.1,
     color: new Color('#ff0000'),
     dashArray: 2, // always has to be the double of the line
     dashOffset: 0, // start the dash at zero
     dashRatio: 0.75, // visible length range min: 0.99, max: 0.5
 });

 // Build the Mesh
 const lineMesh = new Mesh(geometry, material);
 lineMesh.position.x = -4.5;

 // ! Assuming you have your own webgl engine to add meshes on scene and update them.
 webgl.add(lineMesh);

 // ! Call each frame
 function update() {
     // Check if the dash is out to stop animate it.
     if (lineMesh.material.uniforms.dashOffset.value < -2) return;

     // Decrement the dashOffset value to animate the path with the dash.
     lineMesh.material.uniforms.dashOffset.value -= 0.01;
 }