using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBullet : MonoBehaviour {

	private Transform bullet;
	private float speed = 0.3f;

	// Use this for initialization
	void Start () {
		bullet = GetComponent<Transform> ();
	}

	void FixedUpdate(){
		bullet.position += Vector3.up * -speed;

		if (bullet.position.y <= -10)
			Destroy (bullet.gameObject);
	}

	void OnTriggerEnter2D(Collider2D other)
	{
		if (other.tag == "Player") {
			GameObject playerShip = other.gameObject;
			player_controller playerLives = playerShip.GetComponent<player_controller> ();
			playerLives.lives -= 1; //decrement player lives
			Lives.playerLives -= 1;
			Destroy (gameObject);
		} else if (other.tag == "Base") {
			GameObject playerBase = other.gameObject;
			BaseHealth baseHealth = playerBase.GetComponent<BaseHealth> ();
			baseHealth.health -= 1; //decrement base health
			Destroy (gameObject);
		}
	}
}
