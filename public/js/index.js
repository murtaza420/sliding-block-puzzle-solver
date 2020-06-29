const buildPuzzle = () => {
    $('#error-message').addClass("d-none")
    const dimensions = $('#dimensions').val()

    if (!validDimensions(dimensions)) {
        $('#error-message').removeClass("d-none")
        return
    }
    const [x,y] = dimensions.split(",")
    
    let count = 1
    let temp = ""
    for(i = 0; i < x; i++){
        temp += '<div class="puzzle-row">'
        for(j = 0; j < y; j++){
            temp += buildSquare(count)
            count++;
        }
        temp += "</div><br/>"
    }
    $('#puzzle-board').html(temp)
    $('#puzzle-solve').removeClass("d-none")
}

const buildSquare = id => '<input class="puzzle-item" id="' + id + '" type="number"/>'

const validDimensions = dimensions => {
    dim = dimensions.split(",")
    if (dim.length != 2) {
        return false
    }
    return true
}

const solvePuzzle = async () => {
    body = {
        dimensions: $('#dimensions').val()
    }
    const items = $('.puzzle-item')

    for(i = 0; i < items.length; i++){
        body[items[i].getAttribute('id')] = items[i].value
    }

    body['1'] = 1
    body['2'] = -1
    body['3'] = -1
    body['4'] = 1
    body['5'] = 1
    body['6'] = 1
    body['7'] = 0
    body['8'] = 3
    body['9'] = 4
    body['10'] = 1
    body['11'] = 1
    body['12'] = 0
    body['13'] = 2
    body['14'] = 2
    body['15'] = 1
    body['16'] = 1
    body['17'] = 1
    body['18'] = 1
    body['19'] = 1
    body['20'] = 1

    try {
        await fetch('/solve_puzzle', {

            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(body)
        })    
    } catch (error) {
        console.log('ERROR',error)   
    }
}
