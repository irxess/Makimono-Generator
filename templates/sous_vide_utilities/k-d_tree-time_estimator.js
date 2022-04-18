function EstimateTimeNeeded(thicknessMm, temperatureDifferenceC, shapeName) {
    var nearestPoints = undefined;
    if (shapeName == "spherical") {
        nearestPoints = FindNNearestPoints({h: thicknessMm, dT: temperatureDifferenceC }, KD_TREE_SPHERICAL, 3);
    } else if (shapeName == "slab") {
        nearestPoints = FindNNearestPoints({h: thicknessMm, dT: temperatureDifferenceC }, KD_TREE_SLAB, 3);
    } else if (shapeName == "sausage") {
        nearestPoints = FindNNearestPoints({h: thicknessMm, dT: temperatureDifferenceC }, KD_TREE_SAUSAGE, 3);
    } else if (shapeName == "hamburger") {
        nearestPoints = FindNNearestPoints({h: thicknessMm, dT: temperatureDifferenceC }, KD_TREE_HAMBURGER, 3);
    } else {
        throw 'Unrecongnized shape. Consider taking a break before debugging further?';
    }

    var estimateSeconds = FindValueForTInPlaneGivenHAndDT(
        thicknessMm,
        temperatureDifferenceC,
        nearestPoints.flatMap(n => n.point)
    );

    return SecondsToHumanFriendlyTimeString(estimateSeconds);
}

function SecondsToHumanFriendlyTimeString(seconds) {
    // This is not the most generic solution possible, but fits my usecase the best.
    if (seconds >= 360000) {
        // Anything more than maybe 2 or 3 days it too long for the numbers to be actually meaningfull.
        // But it's not really important at that point. So set the cutof here at 100 hours, where the display of the output would become silly.
        return "Error: too long";
    }

    if (seconds < 3600) {
        var minutes = Math.trunc(seconds / 60);
        var seconds = seconds % 60;
        return `${minutes} minutes ${seconds} seconds`;
    }

    var hours = Math.trunc(seconds/3600);
    var minutes = Math.trunc((seconds % 3600) / 60);
    return `${hours} hours ${minutes} minutes`;
}

function FindValueForTInPlaneGivenHAndDT(h, dT, pointsInPlate) {
    // Because the 3 nearest points in the k-d tree can end up being on a line if you've exactly hit a point, check if you've hit a point before bothering with the calculations.
    for (let i = 0; i < pointsInPlate.length; i++) {
        if(pointsInPlate[i].h == h && pointsInPlate[i].dT == dT) {
            return pointsInPlate[i].t;
        }
    }

    var a1 = pointsInPlate[1].h - pointsInPlate[0].h;
    var b1 = pointsInPlate[1].dT - pointsInPlate[0].dT;
    var c1 = pointsInPlate[1].t - pointsInPlate[0].t;
    var a2 = pointsInPlate[2].h - pointsInPlate[0].h;
    var b2 = pointsInPlate[2].dT - pointsInPlate[0].dT;
    var c2 = pointsInPlate[2].t - pointsInPlate[0].t;
    var a = b1 * c2 - b2 * c1;
    var b = a2 * c1 - a1 * c2;
    var c = a1 * b2 - b1 * a2;
    var d = (-a * pointsInPlate[0].h - b * pointsInPlate[0].dT - c * pointsInPlate[0].t);
    // At this point you have all the coefficients for the plane defined by a*x+b*y+c*z+d=0.
    // If you do this outside here, substitute h <-> x, dT <-> y, and t <-> z.
    // Calculate Z:
    return ((a * h + b * dT + d)/(0-c))
}

function FindNNearestPoints(point, kdtree, n = 1) {
    var depth = 0;
    var best = [];
    for (let i = 0; i < n; i++) {
        best.push({
            distance: Infinity,
            point: {
                h: Infinity,
                dT: Infinity,
                t: Infinity
            }
        });
    }
    return FindNearest(point, kdtree, best, 0);
}

function FindNearest(point, currentNode, bestSoFar, depth) {
    // console.log(`Processing node ${JSON.stringify(currentNode?.location)} at depth ${depth} when trying to find ${JSON.stringify(point)}.`);
    if (currentNode == undefined) {
        return bestSoFar;
    }
    // Are we in the top n closest?
    // Note: This requires the `bestSoFar` to have been pre-initialized to have `n` entries (they can all be `undefined` though). It could have been checked here, but it seems wastefull to check it for every iteration considering it will be a solved problem after the first `n` nodes have been visistd.
    var distance = FindDistanceBetweenPoints(point, currentNode.location);
    if(distance < bestSoFar[0].distance) {
        // console.log(`A new best has been found!\nIt beat out ${JSON.stringify(bestSoFar[0])}.\nThe new champion is ${JSON.stringify(currentNode.location)} with distance ${distance}.`);
        bestSoFar[0] = {
            distance: distance,
            point: currentNode.location
        };
        bestSoFar.sort((a,b) => a.distance - b.distance).reverse();
    }

    var k = 2;
    var axis = depth % k;
    if (axis == 0) {
        if(point.h < currentNode.location.h) {
            bestSoFar = FindNearest(point, currentNode.leftChild, bestSoFar, depth + 1);
            if (WorstChildCouldBeBetter(point, bestSoFar, currentNode.location, axis)) {
                bestSoFar = FindNearest(point, currentNode.rightChild, bestSoFar, depth + 1);
            }
        } else {
            bestSoFar = FindNearest(point, currentNode.rightChild, bestSoFar, depth + 1);
            if (WorstChildCouldBeBetter(point, bestSoFar, currentNode.location, axis)) {
                bestSoFar = FindNearest(point, currentNode.leftChild, bestSoFar, depth + 1);
            }
        }
    } else {
        if(point.dT < currentNode.location.dT) {
            bestSoFar = FindNearest(point, currentNode.leftChild, bestSoFar, depth + 1);
            if (WorstChildCouldBeBetter(point, bestSoFar, currentNode.location, axis)) {
                bestSoFar = FindNearest(point, currentNode.rightChild, bestSoFar, depth + 1);
            }
        } else {
            bestSoFar = FindNearest(point, currentNode.rightChild, bestSoFar, depth + 1);
            if (WorstChildCouldBeBetter(point, bestSoFar, currentNode.location, axis)) {
                bestSoFar = FindNearest(point, currentNode.leftChild, bestSoFar, depth + 1);
            }
        }
    }
    return bestSoFar;
}

function FindDistanceBetweenPoints(pointA, pointB) {
    var diffFirstDimention = pointB.h - pointA.h;
    var diffSecondDimention = pointB.dT - pointA.dT;

    var sumDiffsSquared = Math.pow(diffFirstDimention, 2) + Math.pow(diffSecondDimention, 2);
    return sumDiffsSquared;
    // No need to use time to compute root to get actual distance, as long as all comparisons are done using squared distances.
    // return Math.pow(sumDiffsSquared, 0.5);
}

function WorstChildCouldBeBetter(point, bestSoFar, nodeLocation, axis) {
    var axisDistance = NaN;
    if (axis == 0) {
        axisDistance = Math.pow(nodeLocation.h - point.h, 2);
        for (let i = 0; i < bestSoFar.length; i++) {
            if (axisDistance < bestSoFar[i].distance) {
                return true;
            }
        }
    } else {
        axisDistance = Math.pow(nodeLocation.dT - point.dT, 2);
        for (let i = 0; i < bestSoFar.length; i++) {
            if (axisDistance < bestSoFar[i].distance) {
                return true;
            }
        }
    }
    // console.log(`Worst child discarded.\nOur distance² along the ${axis} axis is ${axisDistance}, which is larger than all the best distances² we've ever seen, so the points further away along this axis cannot possibly be any better than the best currently known.\nThe best known distances at the moment are:\n${JSON.stringify(bestSoFar.flatMap(n => n.distance))}`);
    return false;
}
