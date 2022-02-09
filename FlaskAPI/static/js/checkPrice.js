let coin = document.getElementById("selectedCoin")
let amount = document.getElementById("amount")
let output = document.getElementById("calculated")
let button = document.getElementById("check")

button.onclick = function(e)
{
    let value = amount.value.toString()
    let num = coin.value.toString().split("/")[1]
    output.setAttribute("value",(parseFloat(value) * parseFloat(num)).toString())
}