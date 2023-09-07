import React from "react";
import DynamicQuestions from "../DynamicQuestions";
import style from "./style.module.css";
import DynamicQuestions from "../DynamicQuestions";

export default function SymptomForm() {
  return (
    <div className={style["container"]}>
      <DynamicQuestions />
    </div>
  );
}
