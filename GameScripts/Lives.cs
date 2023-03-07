using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Lives : MonoBehaviour {

	public static float playerLives = 5;
	private TextMeshProUGUI livesText;

	// Use this for initialization
	void Start () {
		livesText = GetComponent<TextMeshProUGUI> ();
	}
	
	// Update is called once per frame
	void Update () {
		livesText.text = "Lives: " + playerLives.ToString();
	}
}