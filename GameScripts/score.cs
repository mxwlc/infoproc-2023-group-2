using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class score : MonoBehaviour {

	public static float playerScore = 0;
	private TextMeshProUGUI scoreText;

	// Use this for initialization
	void Start () {
		scoreText = GetComponent<TextMeshProUGUI> ();
	}
	
	// Update is called once per frame
	void Update () {
		scoreText.text = "Score: " + playerScore.ToString();
	}
}