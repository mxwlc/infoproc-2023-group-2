using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InvaderGrid : MonoBehaviour
{

    public Invader[] prefabs; //i think this is from invader.cs animation?
    public GameObject EnemyShot;
    public int rows = 5;
    public int columns = 11;
    public int TotalAmount => rows * columns;
    private Vector3 direction = Vector2.right;
    public float speed = 2.0f; //could change this according to bodycount: more killed->faster if needed
    public int bodycount;
    public int AmountAlive => TotalAmount - bodycount;
    

    /*The { get; private set; } part of the declaration 
    specifies that the property can be read from outside 
    the class (i.e., it has a getter) but can only be set 
    from within the class (i.e., it has a private setter). 
    This means that code outside the class can retrieve 
    the value of totalKilled by calling someInstance.totalKilled, 
    but cannot modify its value directly.*/

    private void Awake()
    {
        // Form the grid of invaders
        for (int i = 0; i < rows; i++)
        {
            float width = 2f * (columns - 1); //spacing * (colum-1) = grid width
            float height = 0.5f * (rows - 1); 

            Vector2 centerOffset = new Vector2(-width /2, -height /2);
            Vector3 rowPosition = new Vector3(centerOffset.x, (2f * i) + centerOffset.y, 0f);

            for (int j = 0; j < columns; j++)
            {
                // Create an invader and parent it to this transform
                Invader invader = Instantiate(prefabs[i], transform);
                invader.invaderGrid = this;
                // Calculate and set the position of the invader in the row
                Vector3 position = rowPosition;
                position.x += 2f * j; //spacing
                invader.transform.localPosition = position; //local: relative to the transform position of parent invader
            }
        }
    }

    private void Attack(){
        int amountAlive = AmountAlive;

        // No missiles should spawn when no invaders are alive
        if (amountAlive == 0) {
            return;
        }

        foreach (Transform invader in transform)
        {
            // Any invaders that are killed cannot shoot missiles
            if (!invader.gameObject.activeInHierarchy) {
                continue;
            }

            if (Random.value < 0.1f)
            {
                Instantiate(EnemyShot, invader.position, Quaternion.identity);
                break; //only one shot per grid each time
            }
        }
    }

    private void Start()
    {
        
        InvokeRepeating("Attack", 1f, 1f);//methodname, time, repeat_rate: invoke method in time second then repeat every repeat_rate seconds
    }

    private void Update()
    {
        
        this.transform.position += direction * speed * Time.deltaTime;
        float leftEdge = -15.5f;
        float rightEdge = 15.5f;
        foreach (Transform invader in this.transform)
        {
            if (invader.position.y <= -6f)
            {
                GameOver.isPlayerDead = true;
                Time.timeScale = 0;
            }
            if (direction == Vector3.right && invader.position.x >= rightEdge){
                GoDownRow();
            }
            else if (direction == Vector3.left && invader.position.x <= leftEdge){
                GoDownRow();
            }
        }
        if (bodycount == (TotalAmount-3)){
            speed *=2;
        }

    }

    private void GoDownRow()
    {
        direction *= -1.0f; //reverse direction
        Vector3 position = this.transform.position;
        position.y -= 0.5f;
        this.transform.position = position;

    }

    private void InvaderKilled()
    {
        bodycount++;
        //score.playerScore += 30; // add to the score
    }


}
