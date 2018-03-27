function permutator(inputArr) {
  var results = [];

  function permute(arr, memo) {
    var cur, memo = memo || [];

    for (var i = 0; i < arr.length; i++) {
      cur = arr.splice(i, 1);
      if (arr.length === 0) {
        results.push(memo.concat(cur));
      }
      permute(arr.slice(), memo.concat(cur));
      arr.splice(i, 0, cur[0]);
    }

    return results;
  }

  return permute(inputArr);
}

function D1(perm) {
	return perm.slice(1)+perm.slice(0,1);
}

function R1(perm) {
  return perm.slice(-1) + perm.slice(0,-1);
}

function DX(x, perm) {
	return perm.slice(x)+perm.slice(0,x).split("").reverse().join("");
}

function RX(x, perm) {
	return perm.slice(-x).split("").reverse().join("")+perm.slice(0,-x);
}

function D2(perm) { return DX(2,perm); }
function D3(perm) { return DX(3,perm); }
function D4(perm) { return DX(4,perm); }
function D5(perm) { return DX(5,perm); }
function D6(perm) { return DX(6,perm); }

function R2(perm) { return RX(2,perm); }
function R3(perm) { return RX(3,perm); }
function R4(perm) { return RX(4,perm); }
function R5(perm) { return RX(5,perm); }
function R6(perm) { return RX(6,perm); }

/*
p = "01234"
console.log(R1(p) + " ⇒ " + p + " ⇒ " + D1(p)) 
console.log(R2(p) + " ⇒ " + p + " ⇒ " + D2(p)) 
console.log(R3(p) + " ⇒ " + p + " ⇒ " + D3(p)) 
console.log(R4(p) + " ⇒ " + p + " ⇒ " + D4(p)) 
console.log(R5(p) + " ⇒ " + p + " ⇒ " + D5(p))//*/
