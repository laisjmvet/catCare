import React, { useState, useEffect } from "react";
import style from "./style.module.css";
import List from "@mui/material/List";
import { useNavigate } from "react-router-dom";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import DoneIcon from "@mui/icons-material/Done";
import Button from "@mui/material/Button";
import { useSymptoms } from "../../contexts";
import { useCredentials } from "../../contexts";
import io from "socket.io-client";

export default function DynamicQuestions() {
  const navigate = useNavigate();
  const [selectedIndex, setSelectedIndex] = React.useState(null);
  const [selectedTick, setSelectedTick] = React.useState(null);
  const [errorText, setErrorText] = useState(false);
  const [socket, setSocket] = useState(null)
  const { dark, setDark } = useCredentials();
  const {
    questionNumber,
    setQuestionNumber,
    answers,
    setAnswers,
    setAnimation,
    animation,
    differentAnswersIndex,
    setDynamicQuestion,
    dynamicQuestion
  } = useSymptoms();

  // Initialize the socket connection when the component mounts
  useEffect(() => {
    const newSocket = io("http://127.0.0.1:5000");

    // Add a "connect" event listener when the socket is created
    newSocket.on("connect", () => {
      console.log("Connected to server");
    });

    // Set the socket and clean up the event listener when the component unmounts
    setSocket(newSocket);
    return () => {
      if (newSocket) {
        newSocket.off("connect");
        newSocket.disconnect();
      }
    };
  }, []);

  const handleListItemClick = (event, index) => {
    setSelectedIndex(index);
    setSelectedTick(index);
    errorText ? setErrorText(false) : null;
  };

  // Function to handle the question event from the server
  const handleQuestion = (questionSocket) => {
    console.log("Received question:", questionSocket);
    setDynamicQuestion(questionSocket)
    console.log(dynamicQuestion, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
  };

  // Register the event listener for the question event
  useEffect(() => {
    if (socket) {
      socket.on("question", handleQuestion);

      // Clean up the previous event listener when the component unmounts
      return () => {
        socket.off("question", handleQuestion);
      };
    }
  }, [socket]);


  const nextQuestion = () => {
    if (selectedTick === null) {
      setErrorText(true);
    } else {
      socket.emit("answer", {
        questionNumber: questionNumber + 1,
        questionID: dynamicQuestion.id,
        answer: selectedIndex + 1,
      });
      setAnswers([...answers, selectedIndex + 1]);
      setAnimation(!animation);
      setQuestionNumber(questionNumber + 1);
      setSelectedTick(null);
      setSelectedIndex(null);
    }
  };

  return (
    <div role="container" className={style["container"]}>
      {questionNumber == 15 ? (
        <>
          <h2
            className={style["end-of-quiz-text"]}
            style={{
              color: dark ? "whitesmoke" : "#121212",
            }}
          >
            It is important that you seek the correct medical help as our
            calculations may not always be correct. You can book a video
            appointment in with one of our vets or see where local vets are in
            your area by clicking on the right button below.
          </h2>
          <div className={style["buttons-container"]}>
            <Button
              variant="contained"
              sx={{
                mt: 4,
                px: 4,
                py: 0.8,
                fontSize: "0.9rem",
                textTransform: "capitalize",
                borderRadius: 1,
                borderColor: "#14192d",
                color: "#fff",
                backgroundColor: "#826BF5",
                "&&:hover": {
                  backgroundColor: "#7958D6",
                },
              }}
              onClick={() => navigate("/video")}
            >
              Book A Video Call
            </Button>
            <Button
              variant="contained"
              sx={{
                mt: 4,
                mb: 4,
                px: 4,
                py: 0.8,
                fontSize: "0.9rem",
                textTransform: "capitalize",
                borderRadius: 1,
                borderColor: "#14192d",
                color: "#fff",
                backgroundColor: "#826BF5",
                "&&:hover": {
                  backgroundColor: "#7958D6",
                },
              }}
              onClick={() => navigate("/map")}
            >
             See A Map of Local Vets
            </Button>
          </div>
        </>
      ) : (
        <>
          <div role="container2">
            <List
              component="nav"
              sx={{ color: dark ? "whitesmoke" : "#121212" }}
              role="list"
            >
              <Divider />
              <ListItemButton
                selected={selectedIndex === 0}
                onClick={(event) => handleListItemClick(event, 0)}
              >
                <ListItemText
                  primary={
                    differentAnswersIndex === questionNumber
                      ? "More than a year"
                      : "No"
                  }
                />
                {selectedTick === 0 ? (
                  <ListItemIcon style={{ color: "green", paddingLeft: "50px" }}>
                    <DoneIcon />
                  </ListItemIcon>
                ) : null}
              </ListItemButton>
              <Divider />
              <ListItemButton
                role="buttons"
                selected={selectedIndex === 1}
                onClick={(event) => handleListItemClick(event, 1)}
              >
                <ListItemText
                  primary={
                    differentAnswersIndex === questionNumber
                      ? "More than six months ago"
                      : "Probably not"
                  }
                />
                {selectedTick === 1 ? (
                  <ListItemIcon style={{ color: "green", paddingLeft: "50px" }}>
                    <DoneIcon />
                  </ListItemIcon>
                ) : null}
              </ListItemButton>
              <Divider />
              <ListItemButton
                role="buttons"
                selected={selectedIndex === 2}
                onClick={(event) => handleListItemClick(event, 2)}
              >
                <ListItemText
                  primary={
                    differentAnswersIndex === questionNumber
                      ? "More than a month ago"
                      : "I don't know"
                  }
                />
                {selectedTick === 2 ? (
                  <ListItemIcon style={{ color: "green", paddingLeft: "50px" }}>
                    <DoneIcon />
                  </ListItemIcon>
                ) : null}
              </ListItemButton>
              <Divider />
              <ListItemButton
                selected={selectedIndex === 3}
                onClick={(event) => handleListItemClick(event, 3)}
              >
                <ListItemText
                  primary={
                    differentAnswersIndex === questionNumber
                      ? "A week to a month ago"
                      : "Probably yes"
                  }
                />
                {selectedTick === 3 ? (
                  <ListItemIcon style={{ color: "green", paddingLeft: "50px" }}>
                    <DoneIcon />
                  </ListItemIcon>
                ) : null}
              </ListItemButton>
              <Divider />
              <ListItemButton
                role="buttons"
                selected={selectedIndex === 4}
                onClick={(event) => handleListItemClick(event, 4)}
              >
                <ListItemText
                  primary={
                    differentAnswersIndex === questionNumber
                      ? "Less than a week ago"
                      : "Yes"
                  }
                />
                {selectedTick === 4 ? (
                  <ListItemIcon style={{ color: "green", paddingLeft: "50px" }}>
                    <DoneIcon />
                  </ListItemIcon>
                ) : null}
              </ListItemButton>
              <Divider />
            </List>
          </div>
          <div role="container3" className={style["button-container"]}>
            <Button
              variant="contained"
              sx={{
                mt: 4,
                mb: !errorText ? 4 : null,
                px: 4,
                py: 0.8,
                fontSize: "0.9rem",
                textTransform: "capitalize",
                borderRadius: 1,
                borderColor: "#14192d",
                color: "#fff",
                backgroundColor: "#826BF5",
                "&&:hover": {
                  backgroundColor: "#7958D6",
                },
                "&&:focus": {
                  backgroundColor: "#7958D6",
                },
              }}
              onClick={nextQuestion}
            >
              Submit
            </Button>
            {errorText ? (
              <p className={style["error-text"]}>You must select an answer!</p>
            ) : null}
          </div>
        </>
      )}
    </div>
  );
}
