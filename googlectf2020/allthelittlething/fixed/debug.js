class Debug {
    #username;
    constructor(username="") {
        this.#username = username
    }
    toString() {
        // console.log(1);
        return `debug_${this.#username}`
    }
}

// Extend user object
function load_debug(user) {
    let debug;
    try {
        debug = JSON.parse(window.name);
    } catch (e) {
        return;
    }

    if (debug instanceof Object) {
        user.debug = new Debug(user.username);
        Object.assign(user.debug, debug);
    }
    // console.log(debug);
    // console.log(user);
    if(user.debug.debugUser){
        user.toString = () => user.debug.toString();
    }
    // console.log(user.debug.toString());
    // console.log(Object.prototype.toString.call(user));
    // console.log(Object.prototype.toString.call(user.toString));
    if(user.debug.verbose){
        console.log(user);
        console.log(user.debug);
    }

    if(user.debug.showAll){
        document.querySelectorAll('*').forEach(e=>e.classList.add('display-block'));
    }

    if(user.debug.keepDebug){
        document.querySelectorAll('a').forEach(e=>e.href=append_debug(e.href));
    }else{
        document.querySelectorAll('a').forEach(e=>e.href=remove_debug(e.href));
    }

    window.onerror = e =>alert(e);
}

function append_debug(u){
    const url = new URL(u);
    url.searchParams.append('__debug__', 1);
    return url.href;
}

function remove_debug(u){
    const url = new URL(u);
    url.searchParams.delete('__debug__');
    return url.href;
}