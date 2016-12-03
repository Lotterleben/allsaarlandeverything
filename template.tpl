<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, user-scalable=no">
    <title></title>
    <style type="text/css">
        @import url('https://fonts.googleapis.com/css?family=Bungee');
        @import url('https://fonts.googleapis.com/css?family=Kumar+One+Outline');
        @import url('https://fonts.googleapis.com/css?family=Kumar+One');

        body {
            text-align: left;
            font-family: sans-serif;
        }

        h11 {
            line-height: 70%;
            font-weight: black;
            font-size: 80px;
            font-family: "Kumar One Outline";
            color: #333;
            margin: 0;
            display: inline-block;
            vertical-align: middle;
        }

        h12 {
            line-height: 70%;
            font-weight: black;
            font-size: 120px;
            font-family: "Bungee";
            color: #ff4081;
            margin: 0;
            display: inline-block;
            vertical-align: middle;
        }

        h13 {
            line-height: 90%;
            font-weight: black;
            font-size: 80px;
            font-family: "Kumar One";
            color: #333;
            margin: 0;
            display: inline-block;
            vertical-align: middle;
        }

        p {
            font-weight: lighter;
            font-size: 35px;
            color: #333;
        }

        .center {
            margin: auto;
            margin-top: 50px;
            width: 60%;
            border: 0px solid #73AD21;
            padding: 20px;
        }

        input[type=text] {
            height: 22px;
            width: 70%;
        }

        input[type=submit] {
            height: 22px;
        }

    </style>
</head>
<body>
    <div class="center">
        <div>
            <h11>All</h11> <br>
            <h12>Saarland</h12> <br>
            <h13>Everything</h13> <br>
        </div>
        <br>
        <br>
        <br>
        <form action="/new/thing" method="GET">
          <input type="text" size="50" maxlength="50" name="thing">
          <input type="submit" name="convert" value="convert">
        </form>
        % if (result != {}):
        <p>{{thing}} entspricht
            %if ("area" in result):
                 <b>{{result["area"]}}</b> (km2)
            %end
            %if ("people" in result):
                %if ("area" in result):
                    bzw.
                <b>{{result["people"]}}</b> (Menschen)
                %end
            %end
        Saarland.
        %end
        </p>
    </div> <!-- content -->
</body>
</html>