/*
// This is a script for creating a k-d tree given a point sample.
// The reason that it is in a separate file, rather than bundled up in a hughe one with tons of other k-d tree utilities, is that in our usecase it is more efficient to pre-compute the k-d tree, and thus thesea are bytes that don't have to be shipped to the browser.

// Sample input data:
var points = [
    { h: 1, dT: 2, t: 20 },
    { h: 1, dT: 3, t: 25 },
    { h: 1, dT: 4, t: 60 },
    { h: 1, dT: 5, t: 400 }
];
// Sample usage
var tree = MakeKDTree(points);
*/

function MakeKDTree(points, depth = 0) {
    // console.log(`We are at depth ${depth}, and have received ${points.length} points.`);
    if (points.length < 1) {
        return undefined;
    }
    // var k = Object.keys(points[0]).length - 1;
    var k = 2; // There are 2 dimensions to consider in our case, thickness and temperature difference.
    var axis = depth % k;
    if (axis == 0) {
        points.sort((a,b) => a.h - b.h);
    } else {
        points.sort((a,b) => a.dT - b.dT);
    }
    var median = Math.trunc(points.length/2);
    return {
        location: points[median],
        leftChild: MakeKDTree(points.slice(0,median), depth + 1),
        rightChild: MakeKDTree(points.slice(median + 1, points.length), depth + 1)
    }
}

function ExportKDTreeAsString(points) {
    var tree = MakeKDTree(points);
    var treeAsString = JSON.stringify(tree);
    console.log(tree);
}
