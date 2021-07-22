let u = new URL(location), p = u.searchParams, k = p.get('keyword') || ''
if ('' === k) history.replaceState('', '', '?keyword=')
axios.get(`/search?keyword=${encodeURIComponent(k)}`).then(resp => {
    result.innerHTML = ''
    for (i of Object.keys(resp.data)) {
        let p = document.createElement('pre')
        p.textContent = resp.data[i]
        result.appendChild(p)
    }
}, err => {
    console.log(err)
    result.innerHTML = '<marquee behavior="alternate"><h1>something is off</h1></marquee><marquee behavior="alternate"><h2>LITERALLY UNPLAYABLE</h2></marquee>'
    result.innerHTML += '<iframe width="560" height="315" src="https://www.youtube.com/embed/lkDUObv5iIU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
})