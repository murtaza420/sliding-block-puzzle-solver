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

const buildSquare = id => '<input class="puzzle-item" id="' + id + '" onchange="inputChangeHandler(this.id)" type="number"/>'

const buildResultSquare = value => {
    const color = getColor(value)
    return '<input class="puzzle-item ' +  color + '" value="' + value + '" disabled/>'
}

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
    body['2'] = 1
    body['3'] = 1
    body['4'] = 1
    body['5'] = 1
    body['6'] = 1
    body['7'] = 3
    body['8'] = 2
    body['9'] = 2
    body['10'] = 1
    body['11'] = 1
    body['12'] = 0
    body['13'] = 4
    body['14'] = 5
    body['15'] = 1
    body['16'] = -1
    body['17'] = 0
    body['18'] = 6
    body['19'] = 7
    body['20'] = 1
    body['21'] = 1
    body['22'] = 1
    body['23'] = 1
    body['24'] = 1
    body['25'] = 1

    try {
        const response = await fetch('/solve_puzzle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(body)
        })
        const output = await response.json()
        renderOutput(output)
        
    } catch (error) {
        console.log('ERROR',error)   
    }
}

const renderOutput = output => {
    const {bfs, dfs, idfs} = output
    const dimensions = $('#dimensions').val()
    const [x, y] = dimensions.split(",")

    $('#bfs-time').text('Time: ' + bfs.time + 's')
    $('#dfs-time').text('Time: ' + dfs.time + 's')
    $('#idfs-time').text('Time: ' + idfs.time + 's')
    
    
    let bfsFinalState = ""
    let dfsFinalState = ""
    let idfsFinalState = ""
    let pos = 1
    for(i = 0; i < x; i++){
        bfsFinalState += '<div class="puzzle-row">'
        dfsFinalState += '<div class="puzzle-row">'
        idfsFinalState += '<div class="puzzle-row">'
        for(j = 0; j < y; j++){
            bfsFinalState += buildResultSquare(bfs['final_state'][pos + ''])
            dfsFinalState += buildResultSquare(dfs['final_state'][pos + ''])
            idfsFinalState += buildResultSquare(idfs['final_state'][pos + ''])
            pos += 1
        }
        bfsFinalState += '</div><br>'
        dfsFinalState += '</div><br>'
        idfsFinalState += '</div><br>'
    }

    $('#bfs-final-state').html(bfsFinalState)
    $('#dfs-final-state').html(dfsFinalState)
    $('#idfs-final-state').html(idfsFinalState)

    $('#results').removeClass('d-none')
}

const inputChangeHandler = id => {
    const value = $('#' + id).val()
    const element = $('#' + id)
    const classes = element.attr('class').split(' ')

    classes.map(c => {
        if (c != 'puzzle-item') {
            console.log(c)
            element.removeClass(c)
        }
    })

    const color = getColor(value)
    element.addClass(color)
}

const getColor = value => {
    if (value == -1) {
        return "green"
    }
    else if (value == 2) {
        return "red"
    }
    else if (value == 0) {
        return "white"
    }
    else if (value == 1) {
        return "grey"
    }
    else if (value > 2) {
        return "yellow"
    }
}