function tmp(i) {
    if (i != 5) {
        console.log(`this is ${i}`);
    } else {
        return;
    }
}


for (let i = 0; i < 10; i++) {
    tmp(i)
}