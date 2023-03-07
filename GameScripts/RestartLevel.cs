using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class RestartLevel : MonoBehaviour {
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.R)) {
			score.playerScore = 0;
			Lives.playerLives = 5;
			GameOver.isPlayerDead = false;
			Time.timeScale = 1;

			SceneManager.LoadScene ("scene_001");
		}
	}
}
